import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Ristoranti } from './ristoranti';

describe('Ristoranti', () => {
  let component: Ristoranti;
  let fixture: ComponentFixture<Ristoranti>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Ristoranti],
    }).compileComponents();

    fixture = TestBed.createComponent(Ristoranti);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
