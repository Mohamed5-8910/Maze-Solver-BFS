const { Counter } = require('./counter');

describe('Counter', () => {
    test('starts with a value of 0', () => {
        const counter = new Counter();

        expect(counter.value).toBe(0);
    });

    test('changes the value to 1 after one increment', () => {
        const counter = new Counter();

        counter.increment();

        expect(counter.value).toBe(1);
    });

    test('changes the value to 2 after two increments', () => {
        const counter = new Counter();

        counter.increment();
        counter.increment();

        expect(counter.value).toBe(2);
    });
});
