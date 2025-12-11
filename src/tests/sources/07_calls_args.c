int inc(int v) { return v + 1; }
int main(void) {
  int x;
  x = inc(3);
  x = inc(inc(x));
  return;
}
