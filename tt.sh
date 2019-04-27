for file in "`pwd`"/**/*.py
do
  #echo "$file"
  sed -i 's/Gaugi.utilities/Gaugi/g' $file
done 


