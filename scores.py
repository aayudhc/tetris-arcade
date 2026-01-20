class Scores:
    points: int
    current_lines_cleared: int
    total_lines_cleared: int

    def __init__(self) -> None:
        self.points = 0
        self.current_lines_cleared = 0
        self.total_lines_cleared = 0

    def record(self) -> None:
        self.current_lines_cleared += 1

    def convert_points(self) -> None:
        self.total_lines_cleared += self.current_lines_cleared

        match self.current_lines_cleared:
            case 1:
                self.points += 40
            case 2:
                self.points += 100
            case 3:
                self.points += 300
            case 4:
                self.points += 1200

        self.current_lines_cleared = 0

    def get_score(self) -> int:
        return self.points

    def get_lines_cleared(self) -> int:
        return self.total_lines_cleared
