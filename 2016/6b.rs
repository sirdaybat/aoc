use std::env;
use std::fs;
use std::io;
use std::io::BufRead;

macro_rules! get(
        ($ex:expr, $err:expr) => (match $ex {
                Some(e) => e,
                None => { println!("{}", $err); return; }
        })
);

macro_rules! get_res(
        ($ex:expr, $err:expr) => (match $ex {
                Ok(v) => v,
                Err(e) => { println!("{}: {}", $err, e); return; }
        })
);

fn solve(file : fs::File){
	let mut counts_at : Vec<[i32; 256]> = Vec::new();

	for line_maybe in io::BufReader::new(&file).lines() {
		let line = get_res!(line_maybe, "can't get line");
		let len = line.len();
		while counts_at.len() < len {
			counts_at.push([0; 256]);
		}
		for (i, c) in line.chars().enumerate() {
			counts_at[i][c as usize] += 1;
		}
	}

	let mut result = String::from("");

	for counts in counts_at {
		let ch = (0..256).filter(|&i| counts[i]>0).min_by_key(|&i| counts[i]).unwrap() as u8 as char;
		result.push(ch);
	}

	println!("{}", result);
}

fn main(){
	let fname = get!(env::args().nth(1), "need args");
	let file = get_res!(fs::File::open(fname), "file not found");

	solve(file);
}
