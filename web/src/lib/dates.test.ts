import { describe, expect, it } from "vitest";
import { dayNumber, daysRemaining, formatDay } from "./dates";

describe("dayNumber", () => {
  it("counts days from 1970-01-01", () => {
    expect(dayNumber("1970-01-01")).toBe(0);
    expect(dayNumber("2026-03-12") - dayNumber("2026-03-11")).toBe(1);
  });

  it("rejects malformed and impossible dates", () => {
    expect(() => dayNumber("2026-3-12")).toThrow(SyntaxError);
    expect(() => dayNumber("2026-02-30")).toThrow(RangeError);
    expect(() => dayNumber("2027-02-29")).toThrow(RangeError);
    expect(dayNumber("2028-02-29")).toBeGreaterThan(0);
  });
});

describe("formatDay", () => {
  it("formats without shifting the day", () => {
    expect(formatDay("2026-03-19")).toBe("19 Mar 2026");
    expect(formatDay("2025-12-31")).toBe("31 Dec 2025");
  });
});

describe("daysRemaining", () => {
  it("counts the last day itself", () => {
    expect(daysRemaining("2026-03-12", "2026-03-19")).toBe(8);
    expect(daysRemaining("2026-03-19", "2026-03-19")).toBe(1);
  });

  it("is zero once quarantine has ended", () => {
    expect(daysRemaining("2026-03-20", "2026-03-19")).toBe(0);
  });

  it("works across a daylight-saving change", () => {
    expect(daysRemaining("2026-03-28", "2026-03-30")).toBe(3);
  });
});
