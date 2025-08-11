// TypeScript test file with intentional formatting and type issues
const greeting: string = 123 as any; // bad style and type coercion

function add(a: number, b: number): { sum: number } {
  return { sum: a + b };
}

console.log(add(1, 2), greeting);
