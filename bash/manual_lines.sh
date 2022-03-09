xls_path=/home/timur/PycharmWork/containers/manual_lines
mkdir "${xls_path}"/csv
mkdir "${xls_path}"/json
# git

for file in "${xls_path}"/*.xls*;
do
    echo "'${file}'";
    csv_name="${xls_path}/csv/$(basename "${file}").csv"
    echo "Will convert Excel '${file}' to CSV '${csv_name}'"
    in2csv "${file}" > "${csv_name}"
    python3 ../scripts/manual_lines.py "${csv_name}" "${xls_path}"/json
done
