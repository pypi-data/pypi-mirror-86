use pyo3::prelude::*;

#[pyfunction]
#[text_signature = "(seq, /)"]
pub fn count(seq: &pyo3::PyAny) -> pyo3::PyResult<u64> {
    let n = seq.len()?;
    let mut inversion: u64 = 0;
    let nn = {
        let mut nn: usize = 1;
        while nn < n {
            nn <<= 1;
        }
        nn-1
    };
    let tree_size = nn*2+1;
    let mut tree = Vec::<usize>::with_capacity(tree_size+1);
    tree.resize(tree_size+1, 0);

    for item in seq.iter()? {
        let item: usize = item?.extract()?;
        if item < 1 || item > n || tree[nn+item]>0 {
            return Err(pyo3::exceptions::PyValueError::new_err("The Sequence has an item not in [1,len(seq)] or duplication"));
        }
        let mut left = nn + item + 1;
        let mut right = nn + n;
        while left <= right {
            if (left&1) == 1 {
                inversion += tree[left] as u64;
            }
            if (right&1) == 0 {
                inversion += tree[right] as u64;
            }
            left = (left+1)>>1;
            right = (right-1)>>1;
        }
        let mut node = nn+item;
        while node != 0 {
            tree[node] += 1;
            node >>= 1;
        }
    }
    Ok(inversion)
}

#[pymodule]
fn python_inversion_number(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(pyo3::wrap_pyfunction!(count, m)?).unwrap();
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        pyo3::Python::with_gil(|py| {
            let list = pyo3::types::PyList::new(py, &[4, 1, 8, 5, 6, 2, 7, 3]);
            let res = super::count(&list);
            assert!(res.is_ok());
            assert!(res.unwrap() == 15_u64);
        })
    }
}
