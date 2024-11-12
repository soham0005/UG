import csv

def read_input_file(filename):
    companies = []
    columns = []
    values = []

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        columns = header[1:]  # Skip the first column (company)

        for row in reader:
            companies.append(row[0])  # First column is company name
            values.append([int(value) for value in row[1:]])

    return companies, columns, values

def calculate_totals(values):
    row_totals = [sum(row) for row in values]
    col_totals = [sum(column) for column in zip(*values)]
    grand_total = sum(row_totals)
    return row_totals, col_totals, grand_total

def save_weights_to_file(output_filename, companies, columns, values, row_totals, col_totals):
    with open(output_filename, mode='w') as file:
        for i, company in enumerate(companies):
            for j, col in enumerate(columns):
                t_weight = (values[i][j] * 100.0) / row_totals[i] if row_totals[i] != 0 else 0
                d_weight = (values[i][j] * 100.0) / col_totals[j] if col_totals[j] != 0 else 0

                # Write each attribute's t-weight and d-weight line by line
                file.write(f"Company: {company}, Product: {col}, Count: {values[i][j]}, "
                           f"t-weight: {t_weight:.2f}%, d-weight: {d_weight:.2f}%\n")

        # Add total weights for each product column
        file.write("\n--- Column Totals ---\n")
        for j, col in enumerate(columns):
            col_total = col_totals[j]
            col_t_weight = (col_total * 100.0) / sum(col_totals) if sum(col_totals) != 0 else 0
            file.write(f"Product: {col}, Total Count: {col_total}, Column t-weight: {col_t_weight:.2f}%, d-weight: 100%\n")

    print(f"Success: Data has been written to {output_filename}")

def main():
    input_filename = "input.csv"
    output_filename = "output.txt"
    
    companies, columns, values = read_input_file(input_filename)
    row_totals, col_totals, grand_total = calculate_totals(values)
    
    # Save t-weight and d-weight line by line in output file
    save_weights_to_file(output_filename, companies, columns, values, row_totals, col_totals)

if __name__ == "__main__":
    main()
