from text_generation import Client

client = Client("http://192.168.16.13:8090")
print(client.generate(f"what is deeplearning?", max_new_tokens=50,seed=0,return_full_text=False,
                      do_sample=False).generated_text)

# text = ""
# for response in client.generate_stream("what is the differnce between mouse and mouse", max_new_tokens=100):
#     if not response.token.special:
#         text += response.token.text
# print(text)