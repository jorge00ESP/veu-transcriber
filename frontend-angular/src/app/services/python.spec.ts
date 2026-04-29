import { TestBed } from '@angular/core/testing';

import { Python } from './python';

describe('Python', () => {
  let service: Python;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Python);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
