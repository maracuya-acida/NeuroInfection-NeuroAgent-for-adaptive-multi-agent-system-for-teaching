#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>

// ── STRUCTURE ─────────────────────────────────────────────────────────────────
// rigor: scale from 1 to 10
//   1-3  → low formal rigor
//   4-6  → medium rigor
//   7-9  → high rigor
//   10   → maximum rigor (e.g. Calculus, Trigonometry)
struct Subject {
    std::string              name;
    std::string              relatedTo;
    std::string              description;
    std::string              difficulty;
    int                      rigor;        // range 1–10
    std::string              prerequisites;
    std::vector<std::string> themes;
    double      (*f32func)(double)            = nullptr;
    long double (*f64func)(long double)       = nullptr;
    float                    f32ulp           = 0.0f;
    float                    f64ulp           = 0.0f;
};

// ── HELPER: prints a Subject ──────────────────────────────────────────────────
void printSubject(const Subject& s) {
    std::cout << "==============================\n";
    std::cout << "Subject      : " << s.name          << "\n";
    std::cout << "Related to   : " << s.relatedTo     << "\n";
    std::cout << "Rigor (1-10) : " << s.rigor         << "\n";
    std::cout << "Description  : " << s.description   << "\n";
    std::cout << "Difficulty   : " << s.difficulty    << "\n";
    std::cout << "Prerequisites: " << s.prerequisites << "\n";
    std::cout << "f32ulp       : " << s.f32ulp        << "\n";
    std::cout << "f64ulp       : " << s.f64ulp        << "\n";

    std::cout << "Themes       : ";
    for (int j = 0; j < (int)s.themes.size(); j++) {
        std::cout << s.themes[j];
        if (j < (int)s.themes.size() - 1) std::cout << ", ";
    }
    std::cout << "\n";
}

// ── HELPER: displays a note based on the rigor level ─────────────────────────
void printRigorNote(const Subject& s) {
    if (s.rigor == 10) {
        std::cout << "[!] " << s.name << " → maximum rigor: "
                  << "requires solid command of formulas and abstract thinking.\n";
    } else if (s.rigor >= 7) {
        std::cout << "[!] " << s.name << " → high rigor: "
                  << "proofs and precise formulation are expected.\n";
    } else if (s.rigor >= 4) {
        std::cout << "[~] " << s.name << " → medium rigor: "
                  << "requires conceptual understanding but less formality.\n";
    } else {
        std::cout << "[ ] " << s.name << " → low rigor: "
                  << "focused on general understanding.\n";
    }
}

// ── MAIN ──────────────────────────────────────────────────────────────────────
int main() {
    std::vector<Subject> listOfSubjects;

    // ── MATH ──────────────────────────────────────────────────────────────────
    Subject math;
    math.name          = "Math";
    math.relatedTo     = "Calculus";
    math.rigor         = 8;            // high rigor, solid formal foundation
    math.description   = "Logical and numerical foundation of sciences";
    math.difficulty    = "VERY HIGH";
    math.prerequisites = "Basic Algebra, Trigonometry";
    math.themes        = {"Algebra", "Trigonometry", "Statistics", "Linear Algebra"};
    math.f32ulp        = 0.5f;
    math.f64ulp        = 1.5f;
    listOfSubjects.push_back(math);

    // ── CALCULUS ──────────────────────────────────────────────────────────────
    Subject calculus;
    calculus.name          = "Calculus";
    calculus.relatedTo     = "Physics";
    calculus.rigor         = 10;       // maximum rigor: limits, epsilon-delta proofs
    calculus.description   = "Branch of math that studies change and accumulation";
    calculus.difficulty    = "HIGH";
    calculus.prerequisites = "Pre-Calculus, Math";
    calculus.themes        = {"Limits", "Derivatives", "Integrals", "Series"};
    calculus.f32ulp        = 0.8f;
    calculus.f64ulp        = 1.2f;
    listOfSubjects.push_back(calculus);

    // ── TRIGONOMETRY ──────────────────────────────────────────────────────────
    Subject trigonometry;
    trigonometry.name          = "Trigonometry";
    trigonometry.relatedTo     = "Math";
    trigonometry.rigor         = 10;   // maximum rigor: identities, proofs, Pythagorean theorem
    trigonometry.description   = "Study of relationships between angles and sides of triangles";
    trigonometry.difficulty    = "HIGH";
    trigonometry.prerequisites = "Basic Algebra, Geometry";
    trigonometry.themes        = {"Unit Circle", "Trigonometric Identities",
                                  "Pythagorean Theorem (a²+b²=c²)", "Inverse Functions"};
    trigonometry.f32ulp        = 0.6f;
    trigonometry.f64ulp        = 1.0f;
    listOfSubjects.push_back(trigonometry);

    // ── PHYSICS ───────────────────────────────────────────────────────────────
    Subject physics;
    physics.name          = "Physics";
    physics.relatedTo     = "Math";
    physics.rigor         = 9;         // very high: requires differential equations
    physics.description   = "Study of the fundamental laws of the universe and matter";
    physics.difficulty    = "HIGH";
    physics.prerequisites = "Calculus, Linear Algebra";
    physics.themes        = {"Mechanics", "Thermodynamics", "Electromagnetism", "Quantum"};
    physics.f32ulp        = 1.0f;
    physics.f64ulp        = 2.0f;
    listOfSubjects.push_back(physics);

    // ── PRINT THE ENTIRE DATABASE ─────────────────────────────────────────────
    std::cout << "\n===== SUBJECT DATABASE =====\n\n";
    for (const Subject& s : listOfSubjects) {
        printSubject(s);
        printRigorNote(s);
        std::cout << "\n";
    }

    // ── SEARCH FOR A THEME ACROSS ALL SUBJECTS ────────────────────────────────
    std::string targetTheme = "Limits";
    std::cout << ">> Searching theme: \"" << targetTheme << "\"\n";

    bool found = false;
    for (const Subject& s : listOfSubjects) {
        for (const std::string& theme : s.themes) {
            if (theme == targetTheme) {
                std::cout << "   Found in: " << s.name
                          << " (rigor: " << s.rigor << ")\n";
                found = true;
            }
        }
    }
    if (!found) {
        std::cout << "   Theme not found in any subject.\n";
    }

    // ── SORT BY RIGOR (highest to lowest) ─────────────────────────────────────
    std::cout << "\n>> Subjects sorted by rigor (high → low):\n";
    std::vector<Subject> sorted = listOfSubjects;
    std::sort(sorted.begin(), sorted.end(),
              [](const Subject& a, const Subject& b) {
                  return a.rigor > b.rigor;
              });
    for (const Subject& s : sorted) {
        std::cout << "   " << s.rigor << "/10  →  " << s.name << "\n";
    }

    return 0;
}
