from .psql import Query


class Acl(object):
    def __init__(self, name, inspect=None, grant=None, revoke=None):
        self.name = name
        self.inspect = inspect
        self._grant = grant
        self._revoke = revoke

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return self.name

    def revoke(self, item):
        yield Query(
            "Revoke %s." % (item,),
            item.dbname,
            self._revoke % dict(
                database=item.dbname,
                schema=item.schema,
                role=item.role,
            ),
        )


class AclItem(object):
    @classmethod
    def from_row(cls, *args):
        return cls(*args)

    def __init__(self, acl, dbname=None, schema=None, role=None):
        self.acl = acl
        self.dbname = dbname
        self.schema = schema
        self.role = role

    def __lt__(self, other):
        return self.as_tuple() < other.as_tuple()

    def __str__(self):
        return '%(acl)s on %(dbname)s.%(schema)s to %(role)s' % dict(
            self.__dict__,
            schema=self.schema or '*'
        )

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def as_tuple(self):
        return (self.acl, self.dbname, self.schema, self.role)


class AclSet(set):
    pass