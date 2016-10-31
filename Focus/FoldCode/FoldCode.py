# written by Michael Mumford
import sublime
import sublime_plugin


class FoldCodeCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.view = view

    def set_regions(self, view, f):
        # passed in list:f is regions to display, not fold.
        # create new region list by switching end points.
        # [(a,b),(c,d),(e,f)] ->  [(b,c),(d,e),(f,end of file)]
        # result is everything not matched by the pattern
        start = 0
        new_region_list = []

        for x in f:
            if start != 0:
                n = sublime.Region(start, x.a - 1)
                new_region_list.append(n)
            start = x.b

        # build the last region, end of file is end point
        z = view.size()
        n = sublime.Region(start, z)
        new_region_list.append(n)

        return new_region_list

    def run(self, edit):
        p = "^(:\\w+[ ]+[0-9.\\w]+)|(#\\w+)"
        f = self.view.find_all(p)
        folds = self.set_regions(self.view, f)

        self.view.fold(folds)
        # after folding, set curser to top of file.
        self.view.set_viewport_position((0.0, 0.0))
        # update status bar
        sublime.status_message("Folded " + str(len(folds)) + " regions")
