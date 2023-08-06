# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from TkinterExtensions import *




def test():
    """ https://stackoverflow.com/questions/7878730/ttk-treeview-alternate-row-colors """
    from random import choice




    colors = ["red", "green", "black", "blue", "white", "yellow", "orange", "pink", "grey", "purple", "brown"]
    def recolor():
        for child in tree.TreeView.get_children():
            picked = choice(colors)
            tree.TreeView.item(child, tags=(picked,), values=(picked,))
        for color in colors:
            tree.TreeView.tag_configure(color, background=color)
        tree.TreeView.tag_configure("red", background="red")


    root = tkRoot(800, 480)
    print('info.patchlevel', root.tk.call('info', 'patchlevel'))

    style = Style(root)
    style.configure("Treeview", foreground="yellow", background="black", fieldbackground="green")

    frame = Frame(root).PlaceFull()
    tree = TreeViewHolderThemed(frame, backgroundColor='white')

    tree.TreeView["columns"] = ("one", "two", "three")
    tree.TreeView.column("#0", width=100, minwidth=30, stretch=Bools.NO)
    tree.TreeView.column("one", width=120, minwidth=30, stretch=Bools.NO)

    tree.TreeView.heading("#0", text="0", anchor=AnchorAndSticky.West)
    tree.TreeView.heading("one", text="1", anchor=AnchorAndSticky.West)

    for i in range(30): tree.TreeView.insert("", i, text=f"Elem {i} ", values="none")

    tree.Pack(side=Side.top, fill=Fill.both, expand=True)

    Button(frame, text="Change").SetCommand(recolor).Pack(fill=tk.X)

    root.mainloop()

def test1():
    from TkinterExtensions.examples import Root
    Root().Run()


def run_all():
    test()
    test1()

if __name__ == '__main__':
    run_all()
