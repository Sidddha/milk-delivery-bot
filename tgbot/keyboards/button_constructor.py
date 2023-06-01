# class Button():
#     def __init__(self, text, callback_data):
#         super().__init__(text=text, callback_data=callback_data)
#         self = {
#             "text": text,
#             "callback_data": callback_data
#         }
# class Button:
#     def __init__(self):
#         self.properties = {}

#     def __setattr__(self, name, value):
#         if isinstance(value, dict) and {"text", "callback_data"}.issubset(value.keys()):
#             self.properties[name] = value
#         else:
#             super().__setattr__(name, value)