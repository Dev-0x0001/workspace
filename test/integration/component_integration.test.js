const { mount } = require('enzyme');
const sinon = require('sinon');
const expect = require('chai').expect;

const { ComponentA } = require('../../../src/components/ComponentA');
const { ComponentB } = require('../../../src/components/ComponentB');

describe('Component Integration', () => {
  let componentA, componentB, clock;

  beforeEach(() => {
    clock = sinon.useFakeTimers();
    componentB = mount(<ComponentB />);
    componentA = mount(<ComponentA onEvent={componentB.instance().handleEvent} />);
  });

  afterEach(() => {
    clock.restore();
    componentA.unmount();
    componentB.unmount();
  });

  it('should trigger event and update state correctly', () => {
    // Arrange
    const spy = sinon.spy(componentB.instance(), 'handleEvent');
    const newValue = 'test value';

    // Act
    componentA.instance().handleInputChange(newValue);
    componentA.simulate('submit');

    // Assert
    expect(spy.calledOnce).to.be.true;
    expect(componentB.state('data')).to.equal(newValue);
    expect(componentB.state('status')).to.equal('updated');
  });

  it('should handle error gracefully', () => {
    // Arrange
    sinon.stub(componentB.instance(), 'handleEvent').throws(new Error('Something went wrong'));

    // Act & Assert
    expect(() => componentA.instance().handleInputChange('error')).not.to.throw();
    expect(componentA.state('errors')).to.have.property('input', 'Something went wrong');
  });
});