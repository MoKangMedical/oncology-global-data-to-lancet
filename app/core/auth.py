"""
用户认证与授权模块
- JWT 认证 (基于标准库实现)
- API 密钥管理
- 使用量追踪
- 配额限制
"""

import hashlib
import hmac
import base64
import json
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from functools import wraps


# ========== 配置 ==========

JWT_SECRET = secrets.token_hex(32)  # 运行时生成，生产环境应从环境变量读取
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

FREE_DAILY_QUOTA = 100  # 免费用户每日调用次数
PAID_DAILY_QUOTA = -1   # 付费用户无限制 (-1 表示无限)


# ========== 内存存储 ==========

users_store: Dict[str, Dict[str, Any]] = {}       # user_id -> user info
api_keys_store: Dict[str, Dict[str, Any]] = {}     # api_key -> key info
usage_store: Dict[str, List[Dict[str, Any]]] = {}  # user_id -> [usage records]


# ========== 密码哈希 ==========

def hash_password(password: str, salt: Optional[str] = None) -> tuple:
    """使用 SHA-256 + salt 哈希密码"""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations=100000
    )
    return hashed.hex(), salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """验证密码"""
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, hashed)


# ========== JWT 实现 ==========

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def _base64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += '=' * padding
    return base64.urlsafe_b64decode(s)


def create_jwt_token(payload: dict) -> str:
    """创建 JWT token"""
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    # 添加过期时间
    now = datetime.utcnow()
    payload.update({
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=JWT_EXPIRE_HOURS)).timestamp())
    })
    header_b64 = _base64url_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = _base64url_encode(json.dumps(payload).encode('utf-8'))
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        JWT_SECRET.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_b64 = _base64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_jwt_token(token: str) -> Optional[dict]:
    """解码并验证 JWT token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, signature_b64 = parts
        # 验证签名
        message = f"{header_b64}.{payload_b64}"
        expected_sig = hmac.new(
            JWT_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        actual_sig = _base64url_decode(signature_b64)
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
        # 解码 payload
        payload = json.loads(_base64url_decode(payload_b64))
        # 检查过期时间
        if payload.get("exp", 0) < datetime.utcnow().timestamp():
            return None
        return payload
    except Exception:
        return None


# ========== 用户管理 ==========

def create_user(username: str, email: str, password: str, plan: str = "free") -> Dict[str, Any]:
    """创建新用户"""
    # 检查用户名是否已存在
    for user in users_store.values():
        if user["username"] == username:
            raise ValueError("用户名已存在")
        if user["email"] == email:
            raise ValueError("邮箱已被注册")

    user_id = f"user_{uuid.uuid4().hex[:12]}"
    hashed, salt = hash_password(password)

    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password_hash": hashed,
        "password_salt": salt,
        "plan": plan,  # "free" or "paid"
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None
    }
    users_store[user_id] = user
    usage_store[user_id] = []
    return _sanitize_user(user)


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """验证用户凭据"""
    for user in users_store.values():
        if user["username"] == username and user["is_active"]:
            if verify_password(password, user["password_hash"], user["password_salt"]):
                user["last_login"] = datetime.utcnow().isoformat()
                return _sanitize_user(user)
    return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """通过 ID 获取用户"""
    user = users_store.get(user_id)
    if user and user["is_active"]:
        return _sanitize_user(user)
    return None


def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    """通过 JWT token 获取用户"""
    payload = decode_jwt_token(token)
    if not payload:
        return None
    return get_user_by_id(payload.get("sub"))


def upgrade_user_plan(user_id: str, plan: str) -> Optional[Dict[str, Any]]:
    """升级用户计划"""
    user = users_store.get(user_id)
    if not user:
        return None
    if plan not in ("free", "paid"):
        raise ValueError("无效的计划类型")
    user["plan"] = plan
    return _sanitize_user(user)


def _sanitize_user(user: dict) -> dict:
    """移除敏感信息"""
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"],
        "plan": user["plan"],
        "is_active": user["is_active"],
        "created_at": user["created_at"],
        "last_login": user["last_login"]
    }


# ========== API 密钥管理 ==========

def generate_api_key(user_id: str, key_name: str = "default") -> Dict[str, Any]:
    """生成 API 密钥"""
    if user_id not in users_store:
        raise ValueError("用户不存在")

    api_key = f"onc_{secrets.token_hex(24)}"
    key_id = f"key_{uuid.uuid4().hex[:8]}"

    key_info = {
        "key_id": key_id,
        "api_key": api_key,
        "user_id": user_id,
        "key_name": key_name,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "last_used": None,
        "usage_count": 0
    }
    api_keys_store[api_key] = key_info
    return key_info


def revoke_api_key(api_key: str) -> bool:
    """撤销 API 密钥"""
    key_info = api_keys_store.get(api_key)
    if key_info:
        key_info["is_active"] = False
        return True
    return False


def revoke_api_key_by_id(user_id: str, key_id: str) -> bool:
    """通过 key_id 撤销用户的 API 密钥"""
    for key_info in api_keys_store.values():
        if key_info["key_id"] == key_id and key_info["user_id"] == user_id:
            key_info["is_active"] = False
            return True
    return False


def validate_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """验证 API 密钥并返回用户信息"""
    key_info = api_keys_store.get(api_key)
    if key_info and key_info["is_active"]:
        user = get_user_by_id(key_info["user_id"])
        if user:
            key_info["last_used"] = datetime.utcnow().isoformat()
            key_info["usage_count"] += 1
            return user
    return None


def list_user_api_keys(user_id: str) -> List[Dict[str, Any]]:
    """列出用户的所有 API 密钥"""
    keys = []
    for key_info in api_keys_store.values():
        if key_info["user_id"] == user_id:
            # 不返回完整 API 密钥，只返回前缀
            safe_key = {**key_info}
            safe_key["api_key_prefix"] = key_info["api_key"][:10] + "..."
            del safe_key["api_key"]
            keys.append(safe_key)
    return keys


# ========== 使用量追踪 ==========

def record_usage(user_id: str, endpoint: str, method: str = "GET",
                 status_code: int = 200, response_time_ms: float = 0):
    """记录 API 调用"""
    if user_id not in usage_store:
        usage_store[user_id] = []

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "response_time_ms": round(response_time_ms, 2)
    }
    usage_store[user_id].append(record)


def get_usage_today(user_id: str) -> int:
    """获取用户今日调用次数"""
    if user_id not in usage_store:
        return 0
    today = datetime.utcnow().date().isoformat()
    return sum(
        1 for r in usage_store[user_id]
        if r["timestamp"].startswith(today)
    )


def get_usage_history(user_id: str, days: int = 7) -> Dict[str, Any]:
    """获取用户使用历史"""
    if user_id not in usage_store:
        return {"total": 0, "daily": {}, "records": []}

    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    recent = [r for r in usage_store[user_id] if r["timestamp"] >= cutoff]

    # 按日统计
    daily = {}
    for r in recent:
        day = r["timestamp"][:10]
        daily[day] = daily.get(day, 0) + 1

    return {
        "total": len(recent),
        "daily": daily,
        "records": recent[-50:]  # 最近 50 条
    }


# ========== 配额限制 ==========

def check_quota(user_id: str) -> Dict[str, Any]:
    """检查用户配额"""
    user = users_store.get(user_id)
    if not user:
        return {"allowed": False, "reason": "用户不存在"}

    plan = user.get("plan", "free")

    if plan == "paid":
        return {
            "allowed": True,
            "plan": "paid",
            "used_today": get_usage_today(user_id),
            "quota": "unlimited"
        }

    # 免费用户检查配额
    used = get_usage_today(user_id)
    if used >= FREE_DAILY_QUOTA:
        return {
            "allowed": False,
            "plan": "free",
            "used_today": used,
            "quota": FREE_DAILY_QUOTA,
            "reason": f"已达到每日调用限制 ({FREE_DAILY_QUOTA}次/天)。升级到付费版以获得无限制访问。"
        }

    return {
        "allowed": True,
        "plan": "free",
        "used_today": used,
        "quota": FREE_DAILY_QUOTA,
        "remaining": FREE_DAILY_QUOTA - used
    }


def get_user_stats(user_id: str) -> Dict[str, Any]:
    """获取用户统计信息"""
    user = users_store.get(user_id)
    if not user:
        return {}

    quota = check_quota(user_id)
    usage_history = get_usage_history(user_id, days=30)
    api_keys = list_user_api_keys(user_id)

    return {
        "user": _sanitize_user(user),
        "quota": quota,
        "api_keys_count": len(api_keys),
        "usage_30d": usage_history["total"],
        "usage_daily": usage_history["daily"]
    }
