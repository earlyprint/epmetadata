bin=$(dirname $0);
cd $bin;
for i in ../tcp_in/*.xml 
do
  fname=$(basename $i);
  b=${fname%.headed.xml}_sourcemeta.xml;
  echo $b;  
  saxon -xsl:../xsl/sourcedesc_extract_tcp2tei.xsl -s:$i -o:../sourcemeta/$b; 
done;
