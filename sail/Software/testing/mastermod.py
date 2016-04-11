import mod1
import mod2

bar_instance = mod1.bar()
bar_instance.printval()
mod2.printval()

bar_instance.foo = "blarg"
bar_instance.printval()
