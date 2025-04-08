def generate_pascals_triangle(n):
    triangle = []
    for i in range(n):
        row = [None] * (i + 1)
        row[0], row[-1] = 1, 1
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle

def main():
    n = int(input("Enter the number of rows for Pascal's triangle: "))
    triangle = generate_pascals_triangle(n)
    for row in triangle:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()