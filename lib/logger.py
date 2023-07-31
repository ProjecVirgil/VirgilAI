
    def Log(self, string: str, filepath: str = None):
        self.__updateCallstack()
        prfx = (Fore.GREEN + f"(in module {self.lastCaller[:-2]}) " + time.strftime("%H:%M:%S UTC LOG", time.localtime()) + Back.RESET + Fore.WHITE)
        prfx = (prfx + " | ")
        log = prfx + string
        if filepath is not None:
            try:
                with open(filepath, "w") as f:
                    f.write(log)
                return ''
            except IOError:
                return log
        return log