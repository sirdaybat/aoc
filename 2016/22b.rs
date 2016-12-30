extern crate regex;
use regex::Regex;
use std::fs;
use std::io;
use std::io::BufRead;
use std::env;
use std::collections::HashSet;

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
	
	let re = Regex::new(r"^/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%$").unwrap();
	
	macro_rules! parse_int(
			($ex:expr) => (get_res!($ex.parse::<i32>(), "syntax error"))
	);

	struct Raw{
		x: u8,
		y: u8,
		size: u16,
		used: u16,
	};
	
	let mut raws = Vec::new();

	for line_maybe in io::BufReader::new(&file).lines() {
		let line = &get_res!(line_maybe, "can't get line");
		
		if let Some(cap) = re.captures(line) {
			let x = parse_int!(cap[1]) as u8;
			let y = parse_int!(cap[2]) as u8;
			let size = parse_int!(cap[3]) as u16;
			let used = parse_int!(cap[4]) as u16;
			raws.push(Raw{ x:x, y:y, size:size, used:used });
		}
	}
	
	let wid = (raws.iter().map(|r| r.x).max().unwrap() as u16) + 1;
	let hei = (raws.iter().map(|r| r.y).max().unwrap() as u16) + 1;
	let nodesnum = wid*hei;
	
	let mut nodesizes = Vec::new();
	nodesizes.resize(nodesnum as usize, 0 as u16);
	
	for raw in &raws {
		nodesizes[(raw.y as u16*wid + raw.x as u16) as usize] = raw.size;
	}
	
	#[derive(Hash, PartialEq, Eq, Clone, Debug)]
	struct State{
		at: u16,
		useds: Vec<u16>,
	};
	
	let newstate = |at| {
		State{ at: at, useds: Vec::new() }
	};
	
	let mut initstate = newstate(wid-1);
	initstate.useds.resize(nodesnum as usize, 0 as u16);
	for raw in &raws {
		initstate.useds[(raw.y as u16*wid + raw.x as u16) as usize] = raw.used;
	}
	
	#[derive(Hash, PartialEq, Eq, Clone, Debug)]
	struct Link{
		from: u16,
		to: u16,
	};
	
	struct AugState{
		state: State,
		links: HashSet<Link>,
	};
	
	let newaugstate = |state| {
		AugState{ state: state, links: HashSet::new() }
	};
	
	let mut initaugstate = newaugstate(initstate.clone());
	
	for y in 0..hei {
		for x in 0..wid {
			let idx = (y*wid + x) as usize;
			for offset in [(1i32, 0), (-1, 0), (0, 1), (0, -1)].iter() {
				let nx = x as i32 + offset.0;
				let ny = y as i32 + offset.1;
				if nx < 0 || nx >= wid as i32 || ny < 0 || ny >= hei as i32 { continue; }
				let nidx = (ny*wid as i32 + nx) as usize;
				if initstate.useds[idx] > 0 && initstate.useds[idx] <= nodesizes[nidx]-initstate.useds[nidx] {
					initaugstate.links.insert(Link{ from: idx as u16, to: nidx as u16 });
				}
			}
		}
	}
	
	let mut queue0 = Vec::new();
	let mut queue1 = Vec::new();
	let mut queue = &mut queue0;
	let mut other_queue = &mut queue1;
	
	let mut visited = HashSet::new();
	
	queue.push(initaugstate);
	visited.insert(initstate.clone());
	
	let mut step = 0;
	
	'mainloop: while queue.len() > 0 {
		step += 1;
	
		'queueloop: for &AugState{ state:ref state, links:ref links } in queue.iter() {
			//println!("ANKKA {:?}", state);
			//println!("..... {:?}", links);
			for &Link{ from:from, to:to } in links {
				let nat = if from == state.at { to } else { state.at };
				
				if nat == 0 {
					println!("FOUND {}", step);
					break 'mainloop;
				}
				
				let mut nuseds = state.useds.clone();
				nuseds[to as usize] += nuseds[from as usize];
				nuseds[from as usize] = 0;
				let mut nlinks = HashSet::new();
				for link in links.iter() {
					if nuseds[link.from as usize] > 0 && nuseds[link.from as usize] <= nodesizes[link.to as usize]-nuseds[link.to as usize] {
						nlinks.insert(link.clone());
					}
				}
				
				let nstate = State{ at:nat, useds:nuseds };
				
				if visited.contains(&nstate) {
					continue;
				}
				
				{
					let x = from%wid;
					let y = from/wid;
					
					for offset in [(1i32, 0), (-1, 0), (0, 1), (0, -1)].iter() {
						let nx = x as i32 + offset.0;
						let ny = y as i32 + offset.1;
						if nx < 0 || nx >= wid as i32 || ny < 0 || ny >= hei as i32 { continue; }
						let nidx = (ny*wid as i32 + nx) as usize;
						if nstate.useds[nidx] > 0 && nstate.useds[nidx] <= nodesizes[from as usize]-nstate.useds[from as usize] {
							nlinks.insert(Link{ from: nidx as u16, to: from });
						}
					}
				}
				{
					let x = to%wid;
					let y = to/wid;
					
					for offset in [(1i32, 0), (-1, 0), (0, 1), (0, -1)].iter() {
						let nx = x as i32 + offset.0;
						let ny = y as i32 + offset.1;
						if nx < 0 || nx >= wid as i32 || ny < 0 || ny >= hei as i32 { continue; }
						let nidx = (ny*wid as i32 + nx) as usize;
						if nstate.useds[to as usize] > 0 && nstate.useds[to as usize] <= nodesizes[nidx]-nstate.useds[nidx] {
							nlinks.insert(Link{ from: to, to: nidx as u16 });
						}
					}
				}
				
				visited.insert(nstate.clone());
				
				let nastate = AugState{ state:nstate, links:nlinks };
				
				other_queue.push(nastate);
				if other_queue.len() > 100000 {
					break 'queueloop;
				}
			}
		}
		
		std::mem::swap(queue, other_queue);
		other_queue.clear();
		
		println!("queue size {}", queue.len());
	}
}
