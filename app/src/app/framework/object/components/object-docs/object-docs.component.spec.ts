import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ObjectDocsComponent } from './object-docs.component';

describe('ObjectDocsComponent', () => {
  let component: ObjectDocsComponent;
  let fixture: ComponentFixture<ObjectDocsComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ObjectDocsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ObjectDocsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
