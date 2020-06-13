import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsAddComponent } from './docapi-settings-add.component';

describe('DocapiSettingsAddComponent', () => {
  let component: DocapiSettingsAddComponent;
  let fixture: ComponentFixture<DocapiSettingsAddComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsAddComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
