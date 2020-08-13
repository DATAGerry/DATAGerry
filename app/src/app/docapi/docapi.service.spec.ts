import { TestBed } from '@angular/core/testing';

import { DocapiService } from './docapi.service';

describe('DocapiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DocapiService = TestBed.get(DocapiService);
    expect(service).toBeTruthy();
  });
});
