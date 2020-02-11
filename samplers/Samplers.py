'''
@author: jcsombria
'''
import random
import time

class Signal(object):

  def sample(self):
    return random.random()

class Sampler(object):
  def __init__(self, signal):
    self.signal = signal
    self.observers = []

  def register(self, o):
    self.observers.append(o)

  def notify(self, data):
    for o in self.observers:
      try:
        o.update(data)
      except:
        pass

  def start(self):
    self.running = True
    while self.running:
      data = self.signal.sample()
      self.notify(data)
      self.wait()

  def stop(self):
    self.running = False

  def wait(self):
    pass

class PeriodicSampler(Sampler):

  def __init__(self, period, signal):
    super().__init__(signal)
    self.Ts = period
    self.reset()

  def notify(self, data):
    data = {
      'timestamp': self.last,
      'value': self.signal.sample(),
    }
    super().notify(data)

  def wait(self):
    # Wait until the next sampling time
    self.last = self.time
    self.time = time.time() - self.t0
    self.next = self.time / self.Ts + self.Ts
    interval = self.Ts - self.time % self.Ts
    time.sleep(interval)

  def sample(self):
    self.signal.sample()

  def reset(self):
    # Reset to the initial state
    self.t0 = time.time()
    self.time = 0
    self.last = 0
    self.next = self.Ts

  def delta(self):
    # Compute the time elapsed since the last sampling time
    return self.time - self.last

  def lastTime(self):
    # Last sampling time
    return self.last


class PeriodicSoD(PeriodicSampler):

  def __init__(self, condition):
    self.condition = condition

  def wait(self):
    event = false
    while not event:
      try:
        event = condition()
      except:
        print('Cannot evaluate sampling condition.')
      super().wait()

