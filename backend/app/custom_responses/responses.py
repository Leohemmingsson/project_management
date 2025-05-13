from ..schemas import ListResponse


def make_list_response(value: list, total: int | None = None) -> ListResponse:
    if total is None:
        response = {"data": value, "total": len(value)}
    else:
        response = {"data": value, "total": total}
    return ListResponse(**response)
