import { TestBed } from '@angular/core/testing';

import { TemplateHelperService } from './template-helper.service';

describe('TemplateHelperService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TemplateHelperService = TestBed.get(TemplateHelperService);
    expect(service).toBeTruthy();
  });
});
