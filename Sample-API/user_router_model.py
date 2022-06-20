from marshmallow import Schema, fields


class BrandGetSchema(Schema):
    ReviewTime_from = fields.Str(example="2021-05-31")
    ReviewTime_to = fields.Str(example="2022-05-31")
    Brand = fields.Str(example='"饗饗","饗泰多" or "all"')

class CorpGetSchema(Schema):
    ReviewTime_from = fields.Str(example="2021-05-31")
    ReviewTime_to = fields.Str(example="2022-05-31")

class PlatformGetSchema(Schema):
    ReviewTime_from = fields.Str(example="2021-05-31")
    ReviewTime_to = fields.Str(example="2022-05-31")

class SearchBranchGetSchema(Schema):
    ReviewTime_from = fields.Str(example="2021-05-31")
    ReviewTime_to = fields.Str(example="2022-05-31")
    Brand = fields.Str(example='"饗饗","饗泰多" or "all"')

class SearchcommentGetSchema(Schema):
    ReviewTime_from = fields.Str(example="2021-05-31")
    ReviewTime_to = fields.Str(example="2022-05-31")
    Brand = fields.Str(example='"饗饗","饗泰多" or "all"')
    ReviewContent = fields.Str(example='好吃')

# Common
class UserCommonResponse(Schema):
    message = fields.Str(example="success")

# Get
class UserGetResponse(UserCommonResponse):
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())
