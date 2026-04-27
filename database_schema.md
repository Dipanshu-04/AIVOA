# Database Schema: AI-First CRM HCP Module

## Overview

This document outlines the MySQL database schema for the AI-first CRM HCP Module, covering the required tables to manage users, HCPs, interactions, audit trails, materials, samples, and follow-ups.

---

## 1. SQL-style Schema Definition

```sql
-- Users (Sales Reps)
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'sales_rep',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Health Care Professionals (HCPs) Master Data
CREATE TABLE hcps (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Interactions (Drafts and Saved)
CREATE TABLE interactions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    hcp_id VARCHAR(36),
    interaction_type VARCHAR(50),
    interaction_date DATE,
    interaction_time TIME,
    attendees TEXT,
    topics_discussed TEXT,
    sentiment VARCHAR(50),
    outcomes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT', -- 'DRAFT' or 'SAVED'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (hcp_id) REFERENCES hcps(id) ON DELETE SET NULL
);

-- Interaction Audit Logs
CREATE TABLE interaction_audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    interaction_id VARCHAR(36) NOT NULL,
    changed_by_user_id VARCHAR(36),
    changed_fields JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Materials Master Data
CREATE TABLE materials (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Samples Master Data
CREATE TABLE samples (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    lot_number VARCHAR(100),
    expiry_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Interaction Materials (Many-to-Many)
CREATE TABLE interaction_materials (
    interaction_id VARCHAR(36) NOT NULL,
    material_id VARCHAR(36) NOT NULL,
    shared_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (interaction_id, material_id),
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
);

-- Interaction Samples (Many-to-Many)
CREATE TABLE interaction_samples (
    interaction_id VARCHAR(36) NOT NULL,
    sample_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    given_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (interaction_id, sample_id),
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE,
    FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE
);

-- Follow-Ups
CREATE TABLE follow_ups (
    id VARCHAR(36) PRIMARY KEY,
    interaction_id VARCHAR(36) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- 'PENDING' or 'COMPLETED'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_hcps_name ON hcps(last_name, first_name);
CREATE INDEX idx_hcps_specialty ON hcps(specialty);
CREATE INDEX idx_interactions_user_id ON interactions(user_id);
CREATE INDEX idx_interactions_hcp_id ON interactions(hcp_id);
CREATE INDEX idx_interactions_status ON interactions(status);
CREATE INDEX idx_audit_logs_interaction_id ON interaction_audit_logs(interaction_id);
CREATE INDEX idx_follow_ups_status_due_date ON follow_ups(status, due_date);
CREATE INDEX idx_follow_ups_interaction_id ON follow_ups(interaction_id);
```
