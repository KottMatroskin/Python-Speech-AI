from __future__ import print_function

from collections import deque
from itertools import islice
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk  # Python 3

try:
    import Queue
except ImportError:
    import queue


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


class Process:

    def __init__(self, root):
        self.root = root
        self.proc = None

        # show subprocess' stdout in GUI
        self._var = tk.StringVar()  # put subprocess output here
        tk.Label( root, bg="#E0E0E0", fg="#000000", activebackground="#A5A5A5", activeforeground="#000000",
                  font=("Ubuntu", 13), textvariable=self._var ).grid( row=4, columnspan=2, sticky="ew" )

        # Creating buttons and Display buttons at startup
        self.b_vc = tk.Button( root, text="Активувати розпізнавання голосу", bg="#E0E0E0", fg="#000000",
                               activebackground="#A5A5A5", activeforeground="#000000", font=("Ubuntu", 13),
                               command=self.start )
        # stop subprocess using a button
        self.b_stop = tk.Button( root, text="Вихід", bg="#E0E0E0", fg="#000000", activebackground="#A5A5A5",
                                 activeforeground="#000000", font=("Ubuntu", 13), command=self.exit )
        self.b_sp = tk.Button( text="Довідник", bg="#E0E0E0", fg="#000000", activebackground="#A5A5A5",
                               activeforeground="#000000", font=("Ubuntu", 13), command=self.about_sw )
        self.b_back = tk.Button( root, text='Назад', bg="#E0E0E0", fg="#000000", activebackground="#A5A5A5",
                                 activeforeground="#000000", font=("Ubuntu", 13), command=self.back_sw )
        self.b_vc.grid( row=1, columnspan=2, sticky="ew" )
        self.b_sp.grid( row=2, columnspan=2, sticky="ew" )
        self.b_stop.grid( row=3, columnspan=2, sticky="ew" )

    def start(self):
        # Stop sab process
        self.stop()
        # start dummy subprocess to generate some output
        self.proc = Popen( ["python", "-u", 'speech_ai.py'], stdout=PIPE, stderr=STDOUT, encoding='utf8' )
        # launch thread to read the subprocess output
        #   (put the subprocess output into the queue in a background thread,
        #    get output from the queue in the GUI thread.
        #    Output chain: proc.readline -> queue -> stringvar -> label)
        q = queue.Queue()
        Thread( target=self.reader_thread, args=[q] ).start()
        self.update( q )  # start update loop

    # About
    def about_sw(self):
        self.b_vc.grid_forget()
        self.b_stop.grid_forget()
        self.b_sp.grid_forget()
        self.b_back.grid( row=1, columnspan=2, sticky="ew" )
        sup_text.grid( row=2, columnspan=2, sticky="ew" )

    # Return back from help
    def back_sw(self):
        sup_text.grid_forget()
        self.b_back.grid_forget()
        self.b_vc.grid( row=1, columnspan=2, sticky="ew" )
        self.b_sp.grid( row=2, columnspan=2, sticky="ew" )
        self.b_stop.grid( row=3, columnspan=2, sticky="ew" )

    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            for line in iter( self.proc.stdout.readline, b'' ):
                q.put( line )
        except ValueError:
            self.proc.wait()

    def update(self, q):
        """Update GUI with items from the queue."""
        # read no more than 10000 lines, use deque to discard lines except the last one,
        for line in deque( islice( iter_except( q.get_nowait, queue.Empty ), 10000 ), maxlen=1 ):
            if line is None:
                return  # stop updating
            else:
                self._var.set( line )  # update GUI
        self.root.after( 40, self.update, q )  # schedule next update

    def stop(self):
        """Stop subprocess and quit GUI."""
        try:
            self.proc.terminate()  # tell the subprocess to exit

            # kill subprocess if it hasn't exited after a countdown
            def kill_after(countdown):
                if self.proc.poll() is None:  # subprocess hasn't exited yet
                    countdown -= 1
                    if countdown < 0:  # do kill
                        self.proc.kill()  # more likely to kill on *nix
                    else:
                        self.root.after( 1000, kill_after, countdown )
                        return  # continue countdown in a second
                # clean up
                self.proc.stdout.close()  # close fd
                self.proc.wait()  # wait for the subprocess' exit
                # self.root.destroy()       # exit GUI

            kill_after( countdown=5 )
        except AttributeError:
            pass

    def exit(self):
        self.stop()
        self.root.destroy()       # exit GUI


# Creating the main window
root = tk.Tk()  # Creating post windows
root.title( "speech_ai_ui" )  # window name
root.resizable( False, False )  # Window size can not be changed

# Creating a description
text = "В голосовому помічнику  'Цирі' реалізований  наступний функціонал:\n-Пошук в мережі інтернет\n" \
       "-Відкривання системних застосунків\n-Відкривання соцмереж\n-ВІдкривання музичних стрімингових " \
       "сервісів\n-Відкривання частовживаних сайтів(вікіпедія,google перекладач)\nДля початку роботи " \
       "натисніть кнопку для активації голосового розпізнавання,потім скажіть необхідну дію,після цього " \
       "очікуйте відповіді.\nЯкщо ваш запит був не розпізнаний,ви отримаєте повідомлення про це."
sup_text = tk.Text( root, height=15, width=40, bg="White", fg="Black", font="Arial 11 bold", wrap=tk.WORD )
sup_text.insert( 1.0, text )

# System sating
app = Process( root )
root.mainloop()  # Starting event processing
