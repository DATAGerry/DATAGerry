import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderComponent } from './docapi-settings-builder.component';

describe('DocapiSettingsBuilderComponent', () => {
  let component: DocapiSettingsBuilderComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
