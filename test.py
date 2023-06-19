from pydantic import BaseModel
"""Test functionality"""


class Base(BaseModel):
    full_amount: int
    invested_amount: int = 0
    closed: bool = False


class Project(Base):
    pass


class Donation(Base):
    pass


projects = [Project(full_amount=400), Project(full_amount=200), Project(full_amount=500)]

donations = [Donation(full_amount=150), Donation(full_amount=300), Donation(full_amount=150), Donation(full_amount=800)]


def val(obj):
    if obj.closed:
        return 0
    return obj.full_amount - obj.invested_amount


def update(projects, donations):
    for donation in donations:
        cur = val(donation)
        for pr in projects:
            if val(pr) > cur:
                pr.invested_amount += cur
                donation.invested_amount = donation.full_amount
                donation.closed = True
                break
            if val(pr) == cur:
                pr.invested_amount += cur
                pr.closed = True
                donation.invested_amount = donation.full_amount
                donation.closed = True
                break
            else:
                donation.invested_amount += val(pr)
                cur = val(donation)
                pr.invested_amount = pr.full_amount
                pr.closed = True


def stats():
    print("=====Projects:")
    for p in projects:
        print(p)
    print("=====Donations:")
    for d in donations:
        print(d)


prs = [p for p in projects if not p.closed]
dons = [d for d in donations if not d.closed]


update(prs, dons)


stats()
