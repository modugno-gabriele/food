import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Fattorini } from './fattorini';

describe('Fattorini', () => {
  let component: Fattorini;
  let fixture: ComponentFixture<Fattorini>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Fattorini],
    }).compileComponents();

    fixture = TestBed.createComponent(Fattorini);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
