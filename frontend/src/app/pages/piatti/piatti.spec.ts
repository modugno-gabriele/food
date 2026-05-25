import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Piatti } from './piatti';

describe('Piatti', () => {
  let component: Piatti;
  let fixture: ComponentFixture<Piatti>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Piatti],
    }).compileComponents();

    fixture = TestBed.createComponent(Piatti);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
