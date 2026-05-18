{
  "calculus": {
    "subject": "Calculus",
    "related_to": "Physics, Trigonometry, Linear Algebra",
    "difficulty": "HIGH",
    "rigor": 10,
    "description": "Branch of mathematics that studies continuous change through derivatives and integrals.",
    "prerequisites": ["Pre-Calculus", "Algebra", "Trigonometry"],

    "topics": {

      "fundamental_theorem_of_calculus": {
        "topic_id": "fundamental_theorem_of_calculus",
        "display_name": "Fundamental Theorem of Calculus — Uniqueness of the Antiderivative",
        "definition": "If `F(x)` is an antiderivative of `f(x)` on an interval `I`, then any other antiderivative `G(x)` of `f(x)` on the same interval satisfies `G(x) = F(x) + k`, where `k` is a real constant.",

        "examples": {
          "antiderivative_basic": {
            "key": "antiderivative_basic",
            "label": "Basic antiderivative verification",
            "given": {
              "F(x)": "`x^3`",
              "f(x)": "`3x^2`"
            },
            "verification": "`F'(x) = 3x^2 = f(x)` ✓"
          }
        },

        "proof": {
          "forward": {
            "description": "If `G(x) = F(x) + k`, then `G` is also an antiderivative of `f`.",
            "formula": {
              "key": "proof_forward_derivative",
              "latex": "`G'(x) = \\frac{d}{dx}\\left[F(x) + k\\right] = F'(x) + 0 = f(x)`"
            }
          },
          "backward": {
            "description": "If both `G` and `F` are antiderivatives of `f`, then `G(x) - F(x)` is constant.",
            "idea": "Define `H(x) = G(x) - F(x)`. Then `H'(x) = 0` on `I`, so `H(x)` is constant (a function with zero derivative on an interval is constant).",
            "formula": {
              "key": "proof_backward_mvt",
              "latex": "`H(b) - H(a) = H'(c)(b - a) = 0 \\cdot (b - a) = 0 \\implies H(b) = H(a)`",
              "note": "Uses the Mean Value Theorem for any `a, b` in `I`."
            }
          }
        },

        "formulas": {
          "general_antiderivative": {
            "key": "general_antiderivative",
            "label": "General form of the antiderivative",
            "latex": "`G(x) = F(x) + C, \\quad C \\in \\mathbb{R}`"
          }
        }
      },

      "substitution_rule": {
        "topic_id": "substitution_rule",
        "display_name": "Integration by Substitution (Change of Variable)",
        "definition": "A technique that simplifies an integral by replacing a composite expression with a single variable `u`, reducing the integrand to a more tractable form.",

        "general_considerations": [
          "Choose `u` so that `du` appears (or is easily related) in the integrand.",
          "The substitution must be differentiable and injective on the interval considered.",
          "Always rewrite the final result in terms of the original variable `x`."
        ],

        "steps": [
          "1. Identify a sub-expression as `u` (typically the inner function of a composition).",
          "2. Compute `du = u' dx`.",
          "3. Rewrite the entire integral in terms of `u`.",
          "4. Integrate with respect to `u`.",
          "5. Back-substitute to express the result in `x`."
        ],

        "common_cases": [
          { "key": "linear_substitution",        "label": "Linear substitution",              "form": "`u = ax + b`" },
          { "key": "trigonometric_substitution",  "label": "Trigonometric substitution",       "form": "`u = sin(x)`, `u = cos(x)`, `u = tan(x)`, etc." },
          { "key": "exponential_substitution",    "label": "Exponential / logarithmic",        "form": "`u = e^x` or `u = ln(x)`" },
          { "key": "radical_substitution",        "label": "Radical substitution",             "form": "`u = \\sqrt{ax + b}`" },
          { "key": "weierstrass_substitution",    "label": "Weierstrass substitution",         "form": "`t = \\tan(x/2)` for integrals of the form `∫ R(sin x, cos x) dx`" }
        ],

        "formulas": {
          "substitution_rule_definite": {
            "key": "substitution_rule_definite",
            "label": "Substitution rule — definite integral",
            "latex": "`\\int_{a}^{b} f(g(x))\\,g'(x)\\,dx = \\int_{g(a)}^{g(b)} f(u)\\,du`"
          },
          "substitution_rule_indefinite": {
            "key": "substitution_rule_indefinite",
            "label": "Substitution rule — indefinite integral",
            "latex": "`\\int f(g(x))\\,g'(x)\\,dx = F(g(x)) + C`"
          }
        }
      },

      "integration_by_parts": {
        "topic_id": "integration_by_parts",
        "display_name": "Integration by Parts",
        "definition": "A technique derived from the product rule for differentiation. Given two continuous and differentiable functions `u(x)` and `v(x)` defined on an open interval, the differential product rule gives `d(uv) = u dv + v du`, which rearranges into the integration-by-parts formula.",

        "derivation": {
          "step_1": {
            "key": "product_rule_differential",
            "label": "Product rule in differential form",
            "latex": "`d(uv) = u\\,dv + v\\,du`"
          },
          "step_2": {
            "key": "rearrangement",
            "label": "Isolate the target term",
            "latex": "`u\\,dv = d(uv) - v\\,du`"
          },
          "step_3": {
            "key": "integrate_both_sides",
            "label": "Integrate both sides",
            "latex": "`\\int u\\,dv = uv - \\int v\\,du + C`"
          }
        },

        "formulas": {
          "integration_by_parts_main": {
            "key": "integration_by_parts_main",
            "label": "Integration by parts — main formula",
            "latex": "`\\int u\\,dv = uv - \\int v\\,du + C`"
          },
          "integration_by_parts_definite": {
            "key": "integration_by_parts_definite",
            "label": "Integration by parts — definite integral",
            "latex": "`\\int_{a}^{b} u\\,dv = \\left[uv\\right]_{a}^{b} - \\int_{a}^{b} v\\,du`"
          }
        },

        "examples": {
          "classic_x_exp": {
            "key": "classic_x_exp",
            "label": "Classic: ∫ x eˣ dx",
            "choice": { "u": "`x`", "dv": "`e^x dx`" },
            "then":   { "du": "`dx`", "v": "`e^x`" },
            "result": "`\\int x e^x dx = x e^x - e^x + C = e^x(x - 1) + C`"
          },
          "ln_x": {
            "key": "ln_x",
            "label": "Natural log: ∫ ln(x) dx",
            "choice": { "u": "`ln(x)`", "dv": "`dx`" },
            "then":   { "du": "`\\frac{1}{x} dx`", "v": "`x`" },
            "result": "`\\int \\ln(x)\\,dx = x\\ln(x) - x + C`"
          }
        }
      },

      "trigonometric_integration": {
        "topic_id": "trigonometric_integration",
        "display_name": "Trigonometric Integration",
        "definition": "Techniques for evaluating integrals that contain trigonometric functions, including powers of sine and cosine, products of trig functions, and integrals solvable via trigonometric identities.",

        "key_identities_used": {
          "pythagorean": {
            "key": "pythagorean_identity",
            "latex": "`\\sin^2(x) + \\cos^2(x) = 1`"
          },
          "half_angle_sin": {
            "key": "half_angle_sin",
            "latex": "`\\sin^2(x) = \\frac{1 - \\cos(2x)}{2}`"
          },
          "half_angle_cos": {
            "key": "half_angle_cos",
            "latex": "`\\cos^2(x) = \\frac{1 + \\cos(2x)}{2}`"
          },
          "product_to_sum": {
            "key": "product_to_sum",
            "latex": "`\\sin(x)\\cos(x) = \\frac{1}{2}\\sin(2x)`"
          }
        },

        "formulas": {
          "integral_sin": {
            "key": "integral_sin",
            "label": "Integral of sin(x)",
            "latex": "`\\int \\sin(x)\\,dx = -\\cos(x) + C`"
          },
          "integral_cos": {
            "key": "integral_cos",
            "label": "Integral of cos(x)",
            "latex": "`\\int \\cos(x)\\,dx = \\sin(x) + C`"
          },
          "integral_sin2": {
            "key": "integral_sin2",
            "label": "Integral of sin²(x) — uses half-angle identity",
            "latex": "`\\int \\sin^2(x)\\,dx = \\frac{x}{2} - \\frac{\\sin(2x)}{4} + C`"
          },
          "integral_cos2": {
            "key": "integral_cos2",
            "label": "Integral of cos²(x) — uses half-angle identity",
            "latex": "`\\int \\cos^2(x)\\,dx = \\frac{x}{2} + \\frac{\\sin(2x)}{4} + C`"
          },
          "integral_tan": {
            "key": "integral_tan",
            "label": "Integral of tan(x)",
            "latex": "`\\int \\tan(x)\\,dx = -\\ln|\\cos(x)| + C`"
          },
          "reduction_formula_sin_n": {
            "key": "reduction_formula_sin_n",
            "label": "Reduction formula for sinⁿ(x)",
            "latex": "`\\int \\sin^n(x)\\,dx = -\\frac{\\sin^{n-1}(x)\\cos(x)}{n} + \\frac{n-1}{n}\\int \\sin^{n-2}(x)\\,dx`"
          }
        },

        "examples": {
          "sin_squared": {
            "key": "sin_squared_example",
            "label": "Evaluate ∫ sin²(x) dx",
            "method": "Apply half-angle identity: `sin²(x) = (1 - cos(2x)) / 2`",
            "result": "`\\int \\sin^2(x)\\,dx = \\frac{x}{2} - \\frac{\\sin(2x)}{4} + C`"
          },
          "sin_cos_product": {
            "key": "sin_cos_product_example",
            "label": "Evaluate ∫ sin(x)cos(x) dx",
            "method": "Use product-to-sum identity: `sin(x)cos(x) = sin(2x)/2`",
            "result": "`\\int \\sin(x)\\cos(x)\\,dx = -\\frac{\\cos(2x)}{4} + C`"
          }
        },

        "pedagogical_connection": {
          "udl_link": "trigonometric_integration_udl",
          "note": "See `pedagogical_methodology.udl_application.trigonometric_integration_udl` for UDL strategies tied to this topic."
        }
      }

    }
  },

  "pedagogical_methodology": {
    "linked_subject": "Calculus",
    "linked_topic": "All calculus topics — especially trigonometric_integration",

    "methods": {
      "concrete_representational_abstract": {
        "key": "CRA",
        "label": "Concrete–Representational–Abstract (CRA)",
        "description": "Learners first manipulate physical or visual objects (concrete), then draw or diagram the concept (representational), and finally work with pure symbols and notation (abstract)."
      },
      "universal_design_for_learning": {
        "key": "UDL",
        "label": "Universal Design for Learning (UDL)",
        "description": "A framework that provides multiple means of engagement, representation, and action/expression so that all learners — including those with diverse cognitive profiles — can access the material.",
        "principles": [
          "Multiple means of representation (visual, auditory, symbolic)",
          "Multiple means of action and expression (written, verbal, graphical)",
          "Multiple means of engagement (choice, relevance, self-regulation)"
        ]
      },
      "3rs_framework": {
        "key": "3Rs",
        "label": "3Rs: Relaxation, Repetition, and Routine",
        "description": "A support framework that lowers anxiety and helps neurodivergent learners (especially those with autism or ADHD) acquire skills through structured calm, spaced repetition, and predictable routines.",
        "target_profile": ["Autism", "ADHD", "Math anxiety"]
      }
    },

    "udl_application": {
      "trigonometric_integration_udl": {
        "key": "trigonometric_integration_udl",
        "topic_ref": "trigonometric_integration",
        "label": "UDL strategies for Trigonometric Integration",
        "representation": [
          "Use the unit circle as a visual anchor before introducing integrals of trig functions.",
          "Show sin²(x) and cos²(x) as areas under curves, not just symbolic expressions.",
          "Color-code each identity used in a derivation step."
        ],
        "action_and_expression": [
          "Allow learners to choose between solving by identity substitution or by reduction formulas.",
          "Provide worked examples with each formula key explicitly labeled (`integral_sin2`, `reduction_formula_sin_n`).",
          "Encourage drawing the graph of the integrand before integrating."
        ],
        "engagement": [
          "Connect trig integration to real-world signals (sound waves, alternating current) for relevance.",
          "Use 3Rs routine: begin each session with a known integral (relaxation), drill identities (repetition), follow a fixed step sequence (routine).",
          "Break the topic into micro-goals: master `integral_sin` and `integral_cos` before tackling powers."
        ]
      }
    }
  }
}
