import { TestBed } from '@angular/core/testing';

import { Evaluacion } from './evaluacion';

describe('Evaluacion', () => {
  let service: Evaluacion;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Evaluacion);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
