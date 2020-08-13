import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsEditComponent } from './docapi-settings-edit.component';

describe('DocapiSettingsEditComponent', () => {
  let component: DocapiSettingsEditComponent;
  let fixture: ComponentFixture<DocapiSettingsEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
