use criterion::{black_box, criterion_group, criterion_main, Criterion};
use python_inversion_number::count;

fn get_random_permutation(n: usize) -> Vec<usize> {
    use rand::seq::SliceRandom;
    use rand::thread_rng;

    let mut rng = thread_rng();
    let mut a:Vec<usize> = (1..=n).collect();
    a.shuffle(&mut rng);
    a
}

pub fn criterion_benchmark(c: &mut Criterion) {
    let mut group = c.benchmark_group("count");
    group.plot_config(criterion::PlotConfiguration::default().summary_scale(criterion::AxisScale::Logarithmic));

    for n in &[1, 2, 3, 5, 10, 100, 1_000, 10_000, 100_000, 1_000_000_usize] {
        pyo3::Python::with_gil(|py| {
            group.bench_with_input(criterion::BenchmarkId::from_parameter(n), n, |b, &n| {
                let a = get_random_permutation(n);
                let list = pyo3::types::PyList::new(py, &a);
                b.iter(|| count(black_box(list)))
            });
        })
    }
    group.finish();
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
