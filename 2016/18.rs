use std::string::*;

fn printline(line: &Vec<char>){
	println!("{}", line.iter().map(|&c| c).collect::<String>());
}

fn count_safes(line: &Vec<char>) -> i32{
	line.iter().map(|&c| (c == '.') as i32).sum()
}

fn main() {
	let mut line : Vec<char> = String::from("^.....^.^^^^^.^..^^.^.......^^..^^^..^^^^..^.^^.^.^....^^...^^.^^.^...^^.^^^^..^^.....^.^...^.^.^^.^").into_bytes().iter().map(|&c| c as char).collect();
	
	let mut total_safes = 0;
	
	for _ in 0..400000-1 {
		printline(&line);
		total_safes += count_safes(&line);
		let mut newline = Vec::new();
		while newline.len() < line.len() {
			let left = if newline.len() > 0 { line[newline.len()-1] } else { '.' };
			let center = line[newline.len()];
			let right = if newline.len()+1 < line.len() { line[newline.len()+1] } else { '.' };
			newline.push(match (left, center, right) {
				('^', '^', '.') => '^',
				('.', '^', '^') => '^',
				('^', '.', '.') => '^',
				('.', '.', '^') => '^',
				_ => '.',
			});
		}
		line = newline;
	}
	
	printline(&line);
	total_safes += count_safes(&line);
	
	println!("{}", total_safes)
}
