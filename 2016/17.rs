extern crate crypto; // rust-crypto 0.2.36
use crypto::md5::Md5;
use crypto::digest::Digest;
use std::mem;

fn main() {
	let passcode = String::from("udskfozm");

	let mut hasher = Md5::new();
	
	let offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)];
	let dirnames = [ 'U', 'D', 'L', 'R' ];
	
	struct State{
		x: i8,
		y: i8,
		past: String,
	}
	
	let mut queue0 : Vec<State> = Vec::new();
	let mut queue1 : Vec<State> = Vec::new();
	
	let mut queue = &mut queue0;
	let mut other_queue = &mut queue1;
	
	let mut string_storage = String::new();
	
	queue.push(State{x:0, y:0, past:String::from("")});
	
	'mainloop: while queue.len() > 0 {
		for state in queue.iter() {
			string_storage.clear();
			string_storage += &passcode;
			string_storage += &state.past;
			hasher.input_str(&string_storage);
			let hash_str = hasher.result_str();
			let hash = hash_str.as_bytes();
			hasher.reset();
			//println!("{}", hash);
			
			for nbidx in 0..4 {
				let ch = hash[nbidx] as char;
				if 'b' <= ch && ch <= 'f' {
					let nx = state.x + offsets[nbidx].0;
					let ny = state.y + offsets[nbidx].1;
					if nx < 0 || ny < 0 || nx >= 4 || ny >= 4 {
						continue;
					}
					
					let mut new_past = state.past.clone();
					new_past += &dirnames[nbidx].to_string();
					
					if nx == 3 && ny == 3 {
						println!("FOUND {} {}", new_past, new_past.len());
						//break 'mainloop;
					}
					else{
						other_queue.push(State{
							x: nx,
							y: ny,
							past: new_past,
						});
					}
				}
			}
		}
		
		queue.clear();
		mem::swap(queue, other_queue);
		
		println!("{}", queue.len());
	}
	
	//let mut 
}
