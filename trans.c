#include <stdio.h>

int main(){
  int size_long;
  int size_int;
  int size_char;

  long a = 0xffff;

  int string_len = 12;
  
  char string[] = "1234";
  
  FILE * target_file = fopen("targetfile","wb");

  printf("%ld\n",a);

  fprintf(target_file,"%ld%d%s",a,string_len,string);
  
  fclose(target_file);

  FILE * source_file = fopen("targetfile","rb");

  long b = 0;

  fscanf(source_file,"%ld",&b);

  fclose(source_file);

  printf("%ld",b);
}