from appframe import Command, verbose


class CreateCommand(Command):
    """
    Greet a person

    greet
        {person? : name of the person to greet}
    """

    def handle(self):
        person = self.argument("person") or "Peter"
        verbose(1, "Greeting person")
        print(f"Hello {person}")
