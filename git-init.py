import os


print(os.getcwd())

curr_dir =os.getcwd()

array = []
while len(array) < 5:
    if input() == 'exit':
        break;
    else:
        array.append(input())
    
concat_string = curr_dir
         
for element in array:
   concat_string = concat_string+"\\"+element

print(concat_string)

new_path = concat_string.split()

print(*new_path)


new_dir = os.path.join(*new_path)
print(new_dir)

if not os.path.exists(new_dir):
    os.makedirs(new_dir, exist_ok = True)
    print(new_dir," \n Is created!")
else:
    print(new_dir," \n Already exists!")

