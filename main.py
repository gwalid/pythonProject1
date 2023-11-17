from ortools.sat.python import cp_model


def main(board_size):
  model = cp_model.CpModel()
  # Creates the variables.
  # The array index is the column, and the value is the row.
  queens = [model.NewIntVar(0, board_size - 1, "x%i" % i) for i in range(board_size)]
  # Creates the constraints.

  # All rows must be different.
  # The following sets the constraint that all queens are in different rows.
  model.AddAllDifferent(queens)

  # Note: all queens must be in different columns because the indices of queens are all different.

  # The following sets the constraint that no two queens can be on the same diagonal.
  for i in range(board_size):
    # Note: is not used in the inner loop.
    diag1 = []
    diag2 = []
    for j in range(board_size):
      # Create variable array for queens(j) + j.
      q1 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
      diag1.append(q1)
      model.Add(q1 == queens[j] + j)
      # Create variable array for queens(j) - j.
      q2 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
      diag2.append(q2)
      model.Add(q2 == queens[j] - j)
    model.AddAllDifferent(diag1)
    model.AddAllDifferent(diag2)

  # All columns must be different because the indices of queens are all different.
  solver = cp_model.CpSolver()
  solution_printer = SolutionPrinter(queens)
  status = solver.SearchForAllSolutions(model, solution_printer)
  print()
  print('Solutions found : %i' % solution_printer.SolutionCount())


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    self.__solution_count = 0

  def OnSolutionCallback(self):
    self.__solution_count += 1
    for v in self.__variables:
      print('%s = %i' % (v, self.Value(v)), end = ' ')
    print()

  def SolutionCount(self):
    return self.__solution_count




board_size=8
main(board_size)