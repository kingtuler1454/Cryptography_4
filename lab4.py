from email import message
import random
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]


def quadratic_nonresidue(x, module ): # квадратичный невычет поиск
    while (x**(0.5*module-0.5) %module -module)!=-1: #если  x^((module-1)/2) дает -1 при делении на модуль, то это искомый квадратичный невычет
        x+=1
    return x


def search_y(p,q,N): # ищем y удовлетворяющий 3ью шагу алгоритма
    a = quadratic_nonresidue(1,p) # вычисляем первый квадратичный невычет
    b = quadratic_nonresidue(1,q) # вычисляем второй квадратичный невычет
    for y in range(N):  # условие y чтобы он при остатке деления на p дал а, и при остатке деления на q дал b
        if y%p==a and y%q==b:
            return(y)
    print("Выбраны неудачные числа p q для образования y, начнем заново ") # если цикл прошелся, но не нашелся y, легче вернуть 0 и начать заново
    return 0


def encryption(N,y,message):
    cription_message=[]
    for bit in message:
        a=random.randint(0,N) # по условию каждый раз избирается рандомное a до N
        if bit== '1':
            cription_message.append(str(y*a**2 %N)) # если бит =1 то его ширфр это y*(a^2)
        else:
            cription_message.append(str(a**2%N)) # если бит=0 то его шифр просто a^2
    print("\nОбъект B зашифровал сообщение: "+ str(cription_message))
    return cription_message


def start_B(N,y):  # действия объекта B
    print("Объект B получил данные N и y")
    message=input("Введите сообщение которое хотите зашифровать: ")
    message=''.join(format(ord(i), '08b') for i in message) # сообщение переформируем в биты
    print("\nИсходное секретное сообщение:\n"+message)
    return encryption(N,y,message) # зашифруем и вернем А текст
    

def is_even(x):
    return x % 2 == 0 # проверка делимости на два для подсчета якоби числа


def jacobi(a, n):  # подсчет для расшифровки сообщения
    if a == 0:
        return 0
    if a == 1:
        return 1

    e = 0
    a1 = a
    while is_even(a1): # пока четное а
        e += 1  # прибавляем e для дальнейших вычислений
        a1 =a1// 2 

    s = 0 # для вывода числа

    if is_even(e):
        s = 1
    elif n % 8 in {1, 7}:
        s = 1
    elif n % 8 in {3, 5}:
        s = -1

    if n % 4 == 3 and a1 % 4 == 3: #свойство числа якоби
        s *= -1

    n1 = n % a1
    
    if a1 == 1: 
        return s
    else:
        return s * jacobi(n1, a1)


def decryption(cription_message,p):
    message=''
    for bit in cription_message:
        e = jacobi(int(bit), p) # если якоби число равно 1, исхдный бит равен 0
        if e==1:
            message+='0'
        else:
            message+='1'
    return message

       
def start_A():
    y=0 # для дальнейшего цикла чтобы в случае чего появилась возможность выбрать другие числа объекту А
    while y==0:
        p=random.choice(prime_numbers) # объект А выбрал первое рандомное простое число
        prime_numbers.remove(p) # убираем из нашего списка первое число чтобы при выборе второго не наткнуться на первое
        q=random.choice(prime_numbers) # объект А выброл второе второе число 
        print("Объект А выбрал числа: "+str(p)+' и '+str(q))
        N=p*q # ищем n=pq 
        print("Число N = "+str(N))
        y=search_y(p,q, N) 
    print("Получили y="+str(y)) # 3ий шаг методички
    
    chipher=start_B(N,y) # отправляем данные объекту B и получаем зашифрованное соообщение от него
    
    bitmessage=decryption(chipher,p)
    print("\nОбъект А расшифровал сообщение:\n"+bitmessage)

def main():
   start_A()
   


if __name__=='__main__':
    main()