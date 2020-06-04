import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsListComponent } from './docapi-settings-list.component';

describe('DocapiSettingsListComponent', () => {
  let component: DocapiSettingsListComponent;
  let fixture: ComponentFixture<DocapiSettingsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
