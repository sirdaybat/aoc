use std::fs;
use std::io;
use std::io::BufRead;
use std::env;
use std::collections::HashSet;
use std::cmp::max;

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

fn main(){
	let file = get_res!(fs::File::open(get!(env::args().nth(1), "need args")), "can't open file");
	
	let rows = io::BufReader::new(&file)
		.lines()
		.map(|l| l.unwrap())
		.filter(|l| { l.len() > 0})
		.map(|l| l.into_bytes().iter().map(|&b| b as char).collect())
		.collect::<Vec<Vec<char>>>();
		
	let hei = rows.len() as i32;
	let wid = rows[0].len() as i32;

	let startpos = {
		let mut result = (0, 0);
		'startposloop: for y in 0..rows.len() {
			let row = &rows[y];
			for x in 0..row.len() {
				if rows[y][x] == '0' {
					result = (x as i32, y as i32);
					break 'startposloop;
				}
			}
		}
		result
	};
	
	let maxnum = {
		let mut result = '0';
		for row in &rows {
			for &c in row {
				if '0' <= c && c <= '9' {
					result = max(result, c);
				}
			}
		}
		result as i32 - '0' as i32
	};
	
	#[derive(Hash, PartialEq, Eq, Clone)]
	struct State{
		nums: u16,
		pos: (i32, i32),
	};
	
	println!("asdf {:?} {:?} {}", rows, startpos, maxnum);
	
	let mut queue = &mut Vec::new();
	let mut other_queue = &mut Vec::new();
	
	let mut visited = HashSet::new();
	
	let initial_state = State{
		nums: 1,
		pos: startpos,
	};
	
	visited.insert(initial_state.clone());
	queue.push(initial_state);

	let mut step = 0;
	'mainloop: while queue.len() > 0 {
		step += 1;
	
		for state in queue.iter() {
			for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)].iter() {
				let newpos = (state.pos.0 + offset.0, state.pos.1 + offset.1);
				if newpos.0 < 0 || newpos.1 < 0 || newpos.0 >= wid || newpos.1 >= hei {
					continue;
				}
				let c = rows[newpos.1 as usize][newpos.0 as usize];
				if c == '#' {
					continue;
				}
				let newnums = state.nums | {
					if c >= '0' && c <= '9' {
						1u16 << (c as i32 - '0' as i32)
					}
					else {
						0
					}
				};
				
				if newnums == (1u16 << (1+maxnum)) - 1 {
					println!("FOUND {} {}", step, newnums);
					break 'mainloop;
				}
				
				let newstate = State{
					nums: newnums,
					pos: newpos,
				};
				
				if visited.contains(&newstate) {
					continue;
				}
				visited.insert(newstate.clone());
				other_queue.push(newstate);
			}
		};
	
		std::mem::swap(queue, other_queue);
		other_queue.clear();
	}
}
