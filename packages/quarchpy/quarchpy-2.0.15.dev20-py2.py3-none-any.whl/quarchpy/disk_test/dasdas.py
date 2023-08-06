item = "OK\r\n                         >\r\n"

pos = item.find("OK")
print(item[:pos + 2] + "\r\n>\r\n")