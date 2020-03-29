first i didn't quite understand what the problem of this project is, but as i got further into it i found some.
At first i qrote some very simple code to simulate the process, all i did was use some varibles the time.sleep comand and some
functions and thats it, there was no threads in the program and everything ran alright, problems started to come when i tried to
intigrate the threads into my program.
frist problem where do i split up?
while messing around with the code to figure where to put the thread, it occured to me another problem, how would the threads commuicate?
since these threads are off to do their own work how would i update them on what is going on, simply put in this example,
if a barber is working on a customer, how would he look into the waiting room and see if there is anyone waiting?
since it is all in one funcation it can't really do that, i wanted the ablity to do something like shop.lookAtwaitingRoom,
so i had to rewrite the code and make it object oriented.
I had a bit of a hard time figuring out what i could make a class out of, so i had to think of the interactions between all the events that
will happen, so in the end i ended up with a waitingRoom class and a customer class, the waitingRoom class will hold the customers and the customers
will hold information about how long their hair cut will take, i also had them hold information about their names, so it makes debuging a little bit
easier.
It took me some time to figure out if i needed a Barber class or not since i was unsure how the barber will get updated, after some testing and
poking with the code, i figured out that the waitingRoom class should contain a queue of the customers and a list of the barbers.

after some messing around it has come to my attention that after reading the sample code, that my initial approach to the problem albe it was come but will but sufice,
so i'll have a deep look at the notes and revise my approach and start a new.


logs:
    these logs are written after i have some 100 lines of code written down and have it working 80 percent ish.

    ran into problem, can't figure out how to print a final statement where all the threads are done,
    need to ensure all threads are done
    using join() i can make sure all threads are done

    new problem observation, t = thread..... and then t = thread..... might over write the t varible making t.join just on the one instance
    sovle?, by append the threads to threads list before starting them
    yup that ensures that all of them will get joined

    customer count did not match up for a while (i was minusing each customer that leaves), took me a while to figure out, when i had 15 chairs 20 customers coming in and 4 barbers
    no matter how i count, there was always one customer left in the shop at the end of the day,
    turns out that one customer did not get a chair since and left.
    so now i added a missed counter and keep the customer constant

    ran into another problem, the chairs count is getting out of hand, thought i had this done but at times, the shop will end up with more chairs then it stated with
    i shall investgate into this matter.
    seems that if i don't use my .status it works fine, so the live update seems to be messing up the code.
    further testing shows that my way of interating through the barbers list and calling sleep() on each to get the current status is messing up the code,
    i suspect that if i call sleep on a barber it will somehow reset them, because more then one barber will start working on the same customer.
    So need to find another way to get a live update on the barbers status,
    Nope just tested it with the sleep() meathod of updating working fine..... back to square 1??
    seems like the more customers there are the more chairs i'll end up, with 100 customers i ended up with 138 chairs
    looking at events to sovle problem,
    turns out my implementation of queues was to fault, i was append the customers to a list and using List[::-1] to reverse the whole list,
    this way i'll end up with a queue, but i was not updating the customer list so the queue gets refreshed everytime i reverse it, so i'll use the queue module instead.

    problem with join, causeing a wait for tstate lock problem, seems like i am causing a deadlock with the join meathod, after more research it seems that the queue module
    has something to do with it, the get and put seems to cuase deadlock. Turns out how python does queues, i can't use queue.get after join() is called, witch cause's a
    deadlock.
    
