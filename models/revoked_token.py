from config.database  import Base
from sqlalchemy import Column,Integer,String,Boolean

class TokenBlacklist(Base):
    __tablename__ = "revoked_tokens"
    id = Column(Integer,primary_key=True,autoincrement=True)
    jti = Column(String,nullable=False)
    expires_at = Column(Integer,nullable=False)
    revoked = Column(Boolean,nullable=False)


def revoketoken(db,jti,expires_at,revoked):
    token = TokenBlacklist(
        jti = jti,
        expires_at = expires_at,
        revoked = revoked
        )
    db.add(token)
    db.flush()
    return True

def is_revoked(db,jti):
    token = db.query(TokenBlacklist.jti == jti).first()
    return token