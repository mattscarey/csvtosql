# csvtosql
Python library that can convert 2D lists and CSV files to SQL

<p>
This library was made because of the apparent lack of Python libraries that can convert to SQL. This library is used by instatiating the Maker class.

<code>Maker({path/to/CSV},{path/to/outputsql.sql},{tablename})</code>

Currently the library directly supports CSV input, since the CSV is turned into a list immediatly, a little tweaking from within will allow input of 2D lists.

After the table is loaded into memory, the columns are dynamically created (field1, field2, ..., fieldn), the statements are then created. With each statement creation, the values in that row are typechecked to keep the types up to date. Once all the statements are made the types will have the maximum value set eg. VARCHAR("max length found"). Once the statements are made and the types set, the trivial task of piecing everything together is done and the .sql file is written. Currently the library only supports strings, integers, and floats. More will be added in the future.
</p>
